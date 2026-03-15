function previewImage(event) {
        const reader = new FileReader();
        reader.onload = function() {
            const output = document.getElementById('imagePreview');
            // This replaces the SVG icon with an <img> tag
            output.innerHTML = `<img src="${reader.result}" class="w-full h-full object-cover" />`;
        };
        
        if(event.target.files[0]) {
            reader.readAsDataURL(event.target.files[0]);
        }
    }