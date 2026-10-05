import QtQuick 2.15
Rectangle { property bool active: false; property int thickness: 1; property string text: ""; signal clicked; width: 30; height: 30; radius: 15; color: active ? "black" : "white"; Text { anchors.centerIn: parent; text: parent.text; color: parent.active ? "white" : "black" }; MouseArea { anchors.fill: parent; onClicked: parent.clicked() } }
