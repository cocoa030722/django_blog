const workspace = document.getElementById('workspace');
let isDragging = false;
let startX = 0, startY = 0, currentX = 0, currentY = 0;

// 공통 함수로 위치 이동 적용
function moveContent(dx, dy) {
  currentX = dx;
  currentY = dy;
  content.style.transform = `translate(${dx}px, ${dy}px)`;
}

// 마우스/터치 이벤트 핸들러
function startDrag(event) {
  if (event.type === 'mousedown' && event.button !== 1) return; // 중간 버튼만 허용
  isDragging = true;
  startX = (event.clientX || event.touches[0].clientX) - currentX;
  startY = (event.clientY || event.touches[0].clientY) - currentY;
  console.log("드래그 시작 (x:" + startX + ", y:" + startY + ")");
}

function duringDrag(event) {
  if (!isDragging) return;

  const x = event.clientX || event.touches[0].clientX;
  const y = event.clientY || event.touches[0].clientY;
  const dx = x - startX;
  const dy = y - startY;

  moveContent(dx, dy);
}

function endDrag() {
  isDragging = false;
  console.log("드래그 종료");
}

workspace.addEventListener('mousedown', startDrag);
workspace.addEventListener('mousemove', duringDrag);
workspace.addEventListener('mouseup', endDrag);
workspace.addEventListener('mouseleave', endDrag);

workspace.addEventListener('touchstart', startDrag);
workspace.addEventListener('touchmove', duringDrag);
workspace.addEventListener('touchend', endDrag);
workspace.addEventListener('touchcancel', endDrag);