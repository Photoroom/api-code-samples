//
//  Copyright © 2023 Artizans. All rights reserved.
//

const url = 'https://sdk.photoroom.com/v1/segment';

console.error('Please replace with your own apiKey');
const apiKey = "YOUR_API_KEY_HERE";

export async function removeBackground(imageFile: File): Promise<Blob> {
    const formData = new FormData();
    formData.append('image_file', imageFile);

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'X-Api-Key': apiKey
        },
        body: formData
    });

    if (!response.ok) {
        console.error(response.json())
        throw new Error('Network response was not ok');
    }

    const imageBlob: Blob = await response.blob();

    return imageBlob;
}
