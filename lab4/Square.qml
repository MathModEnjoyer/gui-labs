import QtQuick 2.15
Rectangle { property bool active: false; signal clicked; width: 42; height: 30; radius: 6; MouseArea { anchors.fill: parent; onClicked: parent.clicked() } }
