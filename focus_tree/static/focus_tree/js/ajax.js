document.getElementById('request-button').onclick=async() => {
  await saveAllNode();
};

async function saveAllNode(){
  try{
    let csrftoken = getCookie('csrftoken');
    const data = [];

    const nodes = document.querySelectorAll('.node'); // 모든 노드를 선택

    nodes.forEach((node) => {
      const tmp = {};
      tmp.x=parseInt(node.style.getPropertyValue("left")||0, 10);
      tmp.y=parseInt(node.style.getPropertyValue("top")||0, 10);
      tmp.id=node.getAttribute("data-id")
      data.push(tmp);
      console.log(node);
    });

    await fetch(`/focus_tree/ajax/save-all/${treeId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify(data),
      credentials: 'same-origin',
      })

    await fetch(`/focus_tree/endpoint/save-relationship/${treeId}`, {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify(tmpEdgeChanges),
      credentials: 'same-origin',
    }).then(function(response) {
      return response.json();
    }).then(function(receivedData) {
      console.log(receivedData); // this will be a json
      //existNodes 갱신
      nodeInfos=receivedData;
      for (const node in nodeInfos) {
          existNodes[node] = new Node(nodeInfos[node]);
      }

      reRenderTree()
      tmpEdgeChanges = []; // 저장 후 변경 내역 초기화
    });
    
  } catch (error) {
      console.error("실패:", error);
  }
}

    
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}