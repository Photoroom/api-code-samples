[<img width="80" alt="App Icon" src="https://user-images.githubusercontent.com/5090957/222391109-fabc0f10-968e-48fa-ba0d-6582c33cbacf.png">](https://www.photoroom.com)

[![join-slack](https://img.shields.io/badge/Slack-Join%20our%20Slack!-green?logo=slack)](https://join.slack.com/t/photoroomapicommunity/shared_invite/zt-1tlv7t2nq-6IgjksQObyCMW6rPKCksjg)
![api-calls](https://img.shields.io/badge/daily%20API%20calls-2M-brightgreen)
![license](https://img.shields.io/badge/license-MIT-lightgrey)

# PhotoRoom API Code Samples 📸

This repository contains code samples to easily interact with our API.

More details about PhotoRoom's API 👉 https://www.photoroom.com/api

Link to the full documentation 👉 https://docs.photoroom.com/docs/api/

## Web

### Option A - Test the API with a demo webpage

You can clone this repository and locally serve this [demo webpage](https://github.com/PhotoRoom/api-code-samples/web/index.html).

To make it work, just [get your `apiKey`](https://app.photoroom.com/api-dashboard) and add it to the file [remove-background.ts](https://github.com/PhotoRoom/api-code-samples/web/remove-background.ts).

(you will need to run `tsc` in order to update the JavaScript code)

### Option B - Integrate the API in your project

To integrate our API inside your website, just copy/paste the content of the file [remove-background.ts](https://github.com/PhotoRoom/api-code-samples/web/remove-background.ts) into your project.

Then, here's an example of how you can call the API:

```javascript
import { removeBackground } from './remove-background.js';

const fileInput = document.getElementById('fileInput') as HTMLInputElement;
const displayImage = document.getElementById('displayImage') as HTMLImageElement;

fileInput.addEventListener('change', async () => {
    const files = fileInput.files;
    if (files && files.length > 0) {
        try {
            const imageBlob = await removeBackground(files[0]); // 👈 API call is here
            const objectURL = URL.createObjectURL(imageBlob);
            displayImage.src = objectURL;
        } catch (error) {
            console.error('Error:', error);
        }
    }
});
```

## Node

### Option A - Test the API in the Terminal

You can clone this repository and run these two commands in the Terminal:

```shell
$ cd api-code-samples/node
$ node demo.js
```

To make it work, just [get your `apiKey`](https://app.photoroom.com/api-dashboard) and add it to the file [remove-background.js](https://github.com/PhotoRoom/api-code-samples/node/remove-background.js).

### Option B - Integrate the API in your project

To integrate our API inside your app, just copy/paste the content of the file [remove-background.js](https://github.com/PhotoRoom/api-code-samples/node/remove-background.js) into your Node project.

Then, here's an example of how you can call the API:

```javascript
const removeBackground = require('./remove-background');

const imagePath = './path/to/your/image.jpg';
const savePath = './path/where/you/want/to/save/response.jpg';

removeBackground(imagePath, savePath)
    .then(message => {
        console.log(message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
```

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

You can also watch this short demo 🍿

[![](https://img.youtube.com/vi/aC-dk988XGQ/0.jpg)](https://www.youtube.com/watch?v=aC-dk988XGQ)
