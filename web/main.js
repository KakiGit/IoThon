ws = new WebSocket("ws://localhost:9011")
ws.onmessage = function (data) {
    let elements = data.data.split('\n')
    if(elements.length>0){
        $("#pole1").text(elements[0].split(' ')[1])
        if(elements[0].split(' ')[1]>5){
            $("#pole1").css('background-image','url("red.png")')
        } else if(elements[0].split(' ')[1]>1) {
            $("#pole1").css('background-image','url("yellow.png")')
        }
        if(elements.length>1){
            $("#pole2").text(elements[1].split(' ')[1])
            if(elements[1].split(' ')[1]>5){
                $("#pole2").css('background-image','url("red.png")')
            } else if(elements[1].split(' ')[1]>1) {
                $("#pole2").css('background-image','url("yellow.png")')
            }
        }
    }
    
}