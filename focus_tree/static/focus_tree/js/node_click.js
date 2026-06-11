function addAllNodeEvent(){
    const node_click_nodes = document.querySelectorAll('.node'); // 모든 노드를 선택

    node_click_nodes.forEach((node) => {
        let clickTimer = null;
        node.addEventListener('click', () => {
            if (clickTimer) {//더블클릭 케이스
                clearTimeout(clickTimer);
                clickTimer = null;
                handleDoubleClickNode(node);
            } else {//싱글클릭 케이스
                clickTimer = setTimeout(() => {
                    node_click_nodes.forEach(n => n.classList.remove('selected'));
                    node.classList.add('selected');
                    handleSingleClickNode(node);
                    clickTimer = null;
                }, 300);
            }
        });
    });
}

function handleSingleClickNode(node) {
    console.log('handleSingleClickNode');
    const handles = node.querySelectorAll('.handle');
    if (handles.length === 0) {
        createHandles(node);
    } else {
        handles.forEach(handle => handle.style.display = 'block');
    }
}

function createHandles(node) {
    const positions = ['top', 'right', 'bottom', 'left'];
    positions.forEach(pos => {
        const handle = document.createElement('div');
        handle.classList.add('handle', pos);
        handle.draggable = true;

        handle.addEventListener('dragstart', handleDragStart);
        handle.addEventListener('dragend', handleDragEnd);

        node.appendChild(handle);
        setTimeout(() => {
            handle.style.display = 'block';
        }, 0);
    });
}

let draggedHandle = null;

function handleDragStart(event) {
    draggedHandle = event.target;
    event.dataTransfer.setData('text/plain', '');
}

async function handleDragEnd(event) {
    const targetNode = document.elementFromPoint(event.clientX, event.clientY);
    if (targetNode && targetNode !== draggedHandle.parentNode) {
        if(targetNode.classList.contains('node')){//자기 자신이 node인 경우
            const sendData = {
                'parent':draggedHandle.parentNode.dataset.id,
                'child':targetNode.dataset.id
            };//부모 노드-자식 노드
            console.log(`handleDragEnd:${sendData}`);
            existNodes[draggedHandle.parentNode.dataset.id]["children"].push(targetNode.dataset.id);
            tmpEdgeChanges.push(sendData); // 변화 내용을 배열에 저장

            console.log(`${draggedHandle.parentNode.dataset.id} is now parent of ${targetNode.dataset.id}`);
            // Optionally, you can update DOM to reflect this relationship
            reRenderTree()
        }else if(targetNode.parentNode.classList.contains('node')){//부모가 node인 경우
            const sendData = {
                'parent':draggedHandle.parentNode.dataset.id,
                'child':targetNode.parentNode.dataset.id
            };//부모 노드-자식 노드
            console.log(`handleDragEnd:${sendData}`);
            existNodes[draggedHandle.parentNode.dataset.id]["children"].push(targetNode.parentNode.dataset.id);
            tmpEdgeChanges.push(sendData); // 변화 내용을 배열에 저장

            console.log(`${draggedHandle.parentNode.dataset.id} is now parent of ${targetNode.parentNode.dataset.id}`);
            // Optionally, you can update DOM to reflect this relationship
            reRenderTree()
        }
    }
    resetHandles();
}

function resetHandles() {
    document.querySelectorAll('.handle').forEach(handle => handle.style.display = 'none');
    draggedHandle = null;
}

function handleDoubleClickNode(node) {
    const currentNode = existNodes[node.dataset.id];
    document.getElementById('nodeNameText').innerText = currentNode.name;
    if(currentNode.image!=''){
        document.getElementById('nodeImage').innerHTML = `
        <img src="${currentNode.image}" width="64" height="64" alt="ppap">
        `;
    }else{
        document.getElementById('nodeImage').innerHTML = `
        <img src="https://via.placeholder.com/64x64" width="64" height="64" alt="sans">
        `;
    }
    
    document.getElementById('nodeMainText').innerText = currentNode.mainText;
    
    // 모달을 표시
    const myModal = new bootstrap.Modal(document.getElementById('nodeDetailModal'));
    myModal.show();
}

document.addEventListener('DOMContentLoaded', () => {
    const parentElement = document.getElementById('nodeDetailModal');
    const gridItems = parentElement.querySelectorAll('[class*="col-"]'); // 부트스트랩으로 정의한 모든 그리드 요소 찾기
    
    gridItems.forEach(item => {
        item.classList.add('custom-grid-item'); // 각 그리드 요소에 커스텀 클래스 추가
    });
});