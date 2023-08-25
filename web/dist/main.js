var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { removeBackground } from './remove-background.js';
const fileInput = document.getElementById('fileInput');
const displayImage = document.getElementById('displayImage');
fileInput.addEventListener('change', () => __awaiter(void 0, void 0, void 0, function* () {
    const files = fileInput.files;
    if (files && files.length > 0) {
        try {
            const imageBlob = yield removeBackground(files[0]);
            const objectURL = URL.createObjectURL(imageBlob);
            displayImage.src = objectURL;
        }
        catch (error) {
            console.error('Error:', error);
        }
    }
}));
