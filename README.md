<img width="80" alt="App Icon" src="https://user-images.githubusercontent.com/5090957/222391109-fabc0f10-968e-48fa-ba0d-6582c33cbacf.png">

# PhotoRoom API Code Samples 📸

This repository contains code samples to easily interact with our API.

More details about PhotoRoom's API 👉 https://www.photoroom.com/api

Link to the full documentation 👉 https://docs.photoroom.com/docs/api/

## iOS

### Option A - Test the API with an Xcode Playground

You can [download a Playground](https://github.com/PhotoRoom/api-sample-code/tree/main/iOS) that will enable you to easily call our API with a sample image:

<img width="800" alt="remove_background_playground" src="https://user-images.githubusercontent.com/5090957/222199663-cf6a243a-2f35-4cc6-a98f-dfbeff5780cb.png">

To make it work, just [get your `apiKey`](https://app.photoroom.com/api-dashboard) and add it to the Playground:

<img width="800" alt="remove_background_api_key" src="https://user-images.githubusercontent.com/5090957/222204959-4ac17671-3444-46c8-bc33-bc4e9c9a7255.png">

### Option B - Integrate the API in your app

To integrate our API inside your app, just copy/paste the content of the file [RemoveBackground.swift](https://github.com/PhotoRoom/api-sample-code/blob/main/iOS/RemoveBackground.playground/Sources/RemoveBackground.swift) into your Xcode project.

Then, depending on whether you are using Swift Concurrency, you can call either:
```swift
// with Swift Concurrency
Task { @MainActor in
    imageView.image = try await removeBackground(of: yourImage)
}
```

or

```swift
// without Swift Concurrency
removeBackground(of: yourImage) { result in
    switch result {
    case let .success(backgroundRemoved):
        imageView.image = backgroundRemoved
    case let .failure(error):
        // handle the `error`
    }
}
```
