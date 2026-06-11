function createNodeElement(node) {
    const div = document.createElement('div');
    div.className = 'node';
    div.style.left = `${node.positionX}px`;
    div.style.top = `${node.positionY}px`;
    div.dataset.id = node.id;
    div.draggable = true;

    const image = createNodeImage(node);
    div.appendChild(image);

    const name = document.createElement('p');
    name.className = 'nodeName';
    name.innerText = node.name;
    div.appendChild(name);
    
    content.appendChild(div);
}

function createNodeImage(node) {
    const image = document.createElement('img');
    image.className = 'nodeImage';
    if(node.image!=''){
        image.src = node.image;
        image.width = 64;
        image.height = 64;
        image.alt = "ppap";
    }else{
        image.src = "https://via.placeholder.com/64x64";
        image.width = 64;
        image.height = 64;
        image.alt = "sans";
    }
    return image;
}
