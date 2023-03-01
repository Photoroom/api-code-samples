import UIKit

var sampleImage = UIImage(named: "sample_image.jpg")!

Task {
    let backgroundRemoved = try? await removeBackground(of: sampleImage)
}
