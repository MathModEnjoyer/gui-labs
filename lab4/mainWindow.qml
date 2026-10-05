import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15

ApplicationWindow {
    id: root
    visible: true
    width: 1000
    height: 720
    title: "Лабораторная работа 4 — Painter"
    color: "#f5f7fb"

    Rectangle {
        id: toolbar
        anchors.top: parent.top
        width: parent.width
        height: 148
        color: "#26364a"

        property color paintColor: "#33b5e5"
        property int thickness: 4

        Column {
            anchors.centerIn: parent
            spacing: 10
            Row {
                spacing: 8
                anchors.horizontalCenter: parent.horizontalCenter
                Repeater {
                    model: ["#33b5e5", "#99cc00", "#ffbb33", "#ff4444", "#ffffff"]
                    Rectangle {
                        width: 42; height: 30; radius: 6
                        color: modelData
                        border.width: toolbar.paintColor === modelData ? 3 : 1
                        border.color: "white"
                        MouseArea { anchors.fill: parent; onClicked: toolbar.paintColor = modelData }
                    }
                }
            }
            Row {
                spacing: 8
                anchors.horizontalCenter: parent.horizontalCenter
                Repeater {
                    model: [2, 4, 8, 12, 18]
                    Rectangle {
                        width: 42; height: 30; radius: 6
                        color: toolbar.thickness === modelData ? "#ffffff" : "#d9e2ef"
                        Text { anchors.centerIn: parent; text: modelData; color: "#26364a" }
                        MouseArea { anchors.fill: parent; onClicked: toolbar.thickness = modelData }
                    }
                }
                Button {
                    text: "Сохранить сейчас"
                    onClicked: canvas.save()
                }
            }
        }
    }

    Canvas {
        id: canvas
        anchors { top: toolbar.bottom; left: parent.left; right: parent.right; bottom: status.top; margins: 14 }
        property real lastX: 0
        property real lastY: 0
        property bool drawing: false

        function save() { backend.save_canvas(toDataURL("image/png")) }
        onPaint: {
            var ctx = getContext("2d")
            ctx.lineWidth = toolbar.thickness
            ctx.lineCap = "round"
            ctx.strokeStyle = toolbar.paintColor
            ctx.beginPath()
            ctx.moveTo(lastX, lastY)
            ctx.lineTo(paintArea.mouseX, paintArea.mouseY)
            ctx.stroke()
            lastX = paintArea.mouseX
            lastY = paintArea.mouseY
        }
        MouseArea {
            id: paintArea
            anchors.fill: parent
            hoverEnabled: true
            onPressed: { canvas.lastX = mouseX; canvas.lastY = mouseY; canvas.drawing = true }
            onReleased: canvas.drawing = false
            onPositionChanged: if (canvas.drawing) canvas.requestPaint()
        }
    }

    Rectangle {
        id: status
        anchors.bottom: parent.bottom
        width: parent.width
        height: 34
        color: "#e6ebf3"
        Text { id: statusText; anchors.centerIn: parent; text: "Автосохранение каждые 30 секунд"; color: "#26364a" }
    }

    Timer {
        interval: 30000
        repeat: true
        running: true
        onTriggered: canvas.save()
    }
    Connections {
        target: backend
        function onSaved(message) { statusText.text = message }
    }
}
