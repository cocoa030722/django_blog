renderTree();

async function renderTree(){
    //노드 자체의 렌더링
    await renderAllNode(existNodes);
    //노드 간 간선의 렌더링
    await renderAllEdge();
    //노드에 이벤트 연걸
    addAllNodeEvent();// REF:node_create.js

    //원점을 잡기 위한 임시 코드
    const dotElement = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    svg.appendChild(dotElement);
    dotElement.setAttribute('cx', 0);
    dotElement.setAttribute('cy', 0);
    dotElement.setAttribute('r', 10);
}

async function renderAllNode(nodes){
    return new Promise((resolve) => {

        for (const node in nodes) {//in 루프는 (파이썬과 다르게) 키값만을 순화함->불러오눈 건 사용자 몫
            createNodeElement(existNodes[node]);// REF:node_create.js
        }
        
        console.log("Nodes rendered");
        resolve();
      });
}
async function renderAllEdge(){
    //먼저 현존하는 모든 svg 내 요소를 지움
    svg.innerHTML = "";
    
    //모든 노드의 렌더링 이후에 실행되어야만 하는 로직
    return new Promise((resolve) => {
        
        const content = document.getElementById('content');
        Array.from(content.children).forEach(node => {
            if (node.tagName.toLowerCase() === 'div') {
                const currentNode = existNodes[node.dataset.id];
                edgeForAllChlidren(node, currentNode.children);

                existEdges[node.dataset.id] = currentNode.children;

            }
        });
        
        //원점을 잡기 위한 임시 코드
        const dotElement = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        svg.appendChild(dotElement);
        dotElement.setAttribute('cx', 0);
        dotElement.setAttribute('cy', 0);
        dotElement.setAttribute('r', 10);
        
        console.log("Edges rendered");
        resolve();
    });
}

function reRenderTree(){//위치 정보가 손실되는 문제 발생
    //모든 노드 선별해 삭제
    content.querySelectorAll('div').forEach(childDiv => {
      childDiv.remove();
    });

    renderTree();
    
    console.log("reRenderTree");
}

function edgeForAllChlidren(node, children) {
    children.forEach(childId => {
        const childNode = document.querySelector(`div[data-id="${childId}"]`);
        renderEdge(node, childNode)
    });
}

function renderEdge(div, child) {
    const parentEdgeCenters = getDivEdgeCenters(div);
    const childEdgeCenters = getDivEdgeCenters(child);
    drawLine(parentEdgeCenters.bottomCenter.x, parentEdgeCenters.bottomCenter.y, childEdgeCenters.topCenter.x, childEdgeCenters.topCenter.y);
}

document.getElementById('tree-serialization-button').onclick=() => {
    treeSerialization();
};

async function treeSerialization() {
    console.log(`treeSerialization`)
    const response = await fetch('/focus_tree/endpoint/download-tree-html', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify(existNodes),
        credentials: 'same-origin',
    });
    if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
    }
    
    // Read the response stream as a readable stream
    const reader = response.body.getReader();
    const stream = new ReadableStream({
        start(controller) {
            // Function to push stream data into the controller
            function push() {
                // Read the next chunk
                reader.read().then(({ done, value }) => {
                    if (done) {
                        controller.close();
                        return;
                    }
                    // Enqueue the chunk to the controller
                    controller.enqueue(value);
                    push();
                });
            }
            push();
        }
    });
    // Convert stream to a blob
    const responseBlob = await new Response(stream).blob();
    // Create a URL for the blob
    const blobUrl = URL.createObjectURL(responseBlob);
    // Create a link and click to download the file
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href= blobUrl;
    a.download = 'interimFileName.html';
    document.body.appendChild(a);
    a.click();
    // Cleanup
    URL.revokeObjectURL(blobUrl);
    document.body.removeChild(a);
    
    console.log(existNodes);
}

//최대한 건들지 말 것(아무튼 잘 동작함)
function getDivEdgeCenters(div) {
    const divRect = div.getBoundingClientRect();
    const contentRect = content.getBoundingClientRect();//상대좌표를 얻기 위한 작업
    
    const topCenter = { x: (divRect.left-contentRect.left) + (divRect.width-contentRect.width) / 2, y: (divRect.top-contentRect.top) };
    const rightCenter = { x: (divRect.right-contentRect.right), y: (divRect.top-contentRect.top) + (divRect.height-contentRect.height) / 2 };
    const bottomCenter = { x: (divRect.left-contentRect.left) + (divRect.width-contentRect.width) / 2, y: (divRect.bottom-contentRect.bottom) };
    const leftCenter = { x: (divRect.left-contentRect.left), y: (divRect.top-contentRect.top) + (divRect.height-contentRect.height) / 2 };
    return { topCenter, rightCenter, bottomCenter, leftCenter };
}