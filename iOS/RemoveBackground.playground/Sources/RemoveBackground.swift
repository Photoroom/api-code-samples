//
//  Copyright © 2023 Artizans. All rights reserved.
//

import Foundation
import UIKit

// MARK: Remove Background API

#error("Please input your apiKey below")
private let apiKey: String = "YOUR_API_KEY"

private enum K {
    static let hostURL = URL(string: "https://sdk.photoroom.com/v1/segment")!
}

public func removeBackground(
    of image: UIImage
) async throws -> UIImage {
    return try await withCheckedThrowingContinuation { continuation in
        removeBackground(of: image) { result in
            continuation.resume(with: result)
        }
    }
}

@available(*, renamed: "removeBackground(of:)")
public func removeBackground(
    of image: UIImage,
    completionHandler: @escaping (Result<UIImage, RemoveBackgroundError>) -> Void
) {
    guard apiKey.isEmpty == false else {
        completionHandler(.failure(.noAPIKey))
        return
    }

    var request = URLRequest(url: K.hostURL)
    request.httpMethod = "POST"
    request.timeoutInterval = 30.0

    let scale = image.scaled(maxDimensions: CGSize(width: 1000, height: 1000))
    let scaledImage = image.scaled(by: scale)

    guard let media = Media(withImage: scaledImage, forKey: "image_file") else {
        completionHandler(.failure(.invalidData))
        return
    }

    let boundary = generateBoundary()
    let body = createDataBody(with: media, boundary: boundary)

    request.httpBody = body

    request.addValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
    request.addValue(apiKey, forHTTPHeaderField: "X-Api-Key")

    let config = URLSessionConfiguration.default
    let session = URLSession(configuration: config)
    let task = session.dataTask(with: request, completionHandler: { responseData, response, error in
        guard let responseData = responseData,
              let response = response as? HTTPURLResponse, error == nil else {
            completionHandler(.failure(.serverError))
            return
        }

        guard (200 ... 299) ~= response.statusCode else {
            print("statusCode should be 2xx, but is \(response.statusCode)")
            print("response = \(response)")
            completionHandler(.failure(.serverError))
            return
        }

        guard let decodedImage = UIImage(data: responseData) else {
            print("Error decoding server response")
            completionHandler(.failure(.serverError))
            return
        }
        completionHandler(.success(decodedImage))
    })
    task.resume()
}

public enum RemoveBackgroundError: Error {
    case invalidData
    case serverError
    case noAPIKey
}

extension RemoveBackgroundError: LocalizedError {
    public var errorDescription: String? {
        switch self {
        case .invalidData:
            return NSLocalizedString("Data of image is not valid.", comment: "")
        case .serverError:
            return NSLocalizedString("There was a server error.", comment: "")
        case .noAPIKey:
            return NSLocalizedString("There is no key for the PhotoRoom API.", comment: "")
        }
    }
}

// MARK: Private Helpers

private func generateBoundary() -> String {
    return "Boundary-\(NSUUID().uuidString)"
}

private func createDataBody(with media: Media, boundary: String) -> Data {
    let lineBreak = "\r\n"
    var body = Data()

    body.appendString("--\(boundary + lineBreak)")
    body.appendString("Content-Disposition: form-data; name=\"\(media.key)\"; filename=\"\(media.fileName)\"\(lineBreak)")
    body.appendString("Content-Type: \(media.mimeType + lineBreak + lineBreak)")
    body.append(media.data)
    body.appendString(lineBreak)
    body.appendString("--\(boundary)--\(lineBreak)")

    return body
}

private struct Media {
    let key: String
    let fileName: String
    let data: Data
    let mimeType: String

    init?(withImage image: UIImage, forKey key: String) {
        self.key = key
        self.mimeType = "image/jpg"
        self.fileName = "\(arc4random()).jpeg"

        guard let data = image.jpegData(compressionQuality: 0.7) else { return nil }
        self.data = data
    }
}

private extension Data {
    mutating func appendString(_ string: String) {
        let data = string.data(using: .utf8)
        append(data!)
    }
}

private extension UIImage {
    func scaled(by scale: CGFloat) -> UIImage {
        guard let scaledImage = CIImage(image: self)?.scaled(by: scale) else {
            return self
        }
        return UIImage(ciImage: scaledImage, scale: UIScreen.main.scale, orientation: imageOrientation)
    }

    func scaled(maxDimensions: CGSize) -> CGFloat {
        let scale = min(maxDimensions.width / size.width, maxDimensions.height / size.height)
        if scale >= 1 {
            return 1
        }
        return scale
    }
}

private extension CIImage {
    func scaled(by scale: CGFloat) -> CIImage {
        guard scale != 1 else { return self }
        return applyingFilter(
            "CILanczosScaleTransform",
            parameters: [
                kCIInputScaleKey: Float(scale),
                kCIInputAspectRatioKey: 1,
            ]
        )
    }
}
