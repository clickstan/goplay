// ActionScript file
public function tabNavigatorCreated():void {
	createRoom("main");
}


public function createRoom(name:String):void {
	trace("creating the room ",name);
	var nc:NavigatorContent = new NavigatorContent();
	nc.name = name;
	nc.label = name;
	var rc:RoomComponent = new RoomComponent();
	rc.init(name);
	nc.addElement(rc);
	chatRoomNavigator.addChild(nc);
}