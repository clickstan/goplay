// ActionScript file
public function tabNavigatorCreated():void {
	createRoomNavigatorContent("main");
}

public function createRoomBtn():void {
	if (createRoomB.label != "OK") {
		createRoomTxt.visible = true;
		createRoomB.label = "OK"
	} else {
		trace("sending createRoom command name=",createRoomTxt.text);
		var obj:Object = Room.createRoom(createRoomTxt.text);
		conn.send(obj);
		
		createRoomB.label = "Create"
		createRoomTxt.visible = false;
		createRoomTxt.text = "new room"
	}
} 



public function openRoom():void {
	var name:String = roomsGrid.selectedItem.toString();
	var openedNV:Object = chatRoomNavigator.getChildByName(name);
	if (openedNV == null) {
		trace("sending openRoom(",name,")");
		var obj:Object = Room.openRoom(name);
		conn.addResponseHandler(createRoomNavigatorContentCaller, obj.trans);
		conn.send(obj);
	}
}

public function createRoomNavigatorContentCaller(obj:Object):void {
	createRoomNavigatorContent(obj.name);
}

public function createRoomNavigatorContent(name:String):void {
	var openedNV:Object = chatRoomNavigator.getChildByName(name);
	if (openedNV == null) {
		trace("creating the room tab",name);
		var nc:NavigatorContent = new NavigatorContent();
		nc.name = name;
		nc.label = name;
		var rc:RoomComponent = new RoomComponent();
		rc.init(name);
		nc.addElement(rc);
		chatRoomNavigator.addChild(nc);
	}
}


public function createRoomNavigatorContent_ChatOnly(name:String, chat_id:int):void {
	trace("creating the chat tab",name);
	var nc:NavigatorContent = new NavigatorContent();
	nc.name = name;
	nc.label = name;
	var cc:ChatComponent = new ChatComponent();
	cc.init(chat_id);
	nc.addElement(cc);
	chatRoomNavigator.addChild(nc);
}