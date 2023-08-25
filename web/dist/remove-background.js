//
//  Copyright © 2023 Artizans. All rights reserved.
//
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
const url = 'https://sdk.photoroom.com/v1/segment';
console.error('Please replace with your own apiKey');
const apiKey = "YOUR_API_KEY_HERE";
export function removeBackground(imageFile) {
    return __awaiter(this, void 0, void 0, function* () {
        const formData = new FormData();
        formData.append('image_file', imageFile);
        const response = yield fetch(url, {
            method: 'POST',
            headers: {
                'X-Api-Key': apiKey
            },
            body: formData
        });
        if (!response.ok) {
            console.error(response.json());
            throw new Error('Network response was not ok');
        }
        const imageBlob = yield response.blob();
        return imageBlob;
    });
}
