let node_startX=0, node_startY=0;//delta를 측정하는 데 이용
let node_currentX=0, node_currentY=0;//node의 현 위치
let dx=0, dy=0;

let activeNode=null;

content.addEventListener("dragstart", function(event) {
  activeNode=null;
  const targetNode = document.elementFromPoint(event.clientX, event.clientY);
  if (targetNode.classList.contains('node')) {//본인
    activeNode = event.target;
  }else if(targetNode.parentElement.classList.contains('node') && !targetNode.classList.contains('handle')){//handle이 아닌 자식
    activeNode = targetNode.parentElement;
  }
  if(activeNode !== null){
    let topString = activeNode.style.top;
    let leftString = activeNode.style.left;

    let topInt = parseInt(topString||0, 10);
    let leftInt = parseInt(leftString||0, 10);

    node_currentX=leftInt;
    node_currentY=topInt;

    node_startX = event.clientX - node_currentX;
    node_startY = event.clientY - node_currentY;
  }
  
});

content.addEventListener("drag", function(event) {
  
  if(event.clientX > 0){//드래그를 끝내기 직전의 event.clientX는 0이 됨->0 이상인 경우만 반영해야 함
    dx = event.clientX - node_startX;
  }
  if(event.clientY > 0){
    dy = event.clientY - node_startY;
  }
  
  if(activeNode !== null){
    activeNode.style.left=(dx)+"px";
    activeNode.style.top=(dy)+"px";
    existNodes[activeNode.dataset.id].setPosition(dx, dy);
  }
  renderAllEdge()// REF:tree_render.js
});