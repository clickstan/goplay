// ActionScript file
public function tabNavigatorCreated():void {
	createRoom("Main");
}


public function createRoom(name:String):void {
	trace("creating the room ",name);
	var nc:NavigatorContent = new NavigatorContent();
	nc.name = name;
	nc.label = name;
	var rc:RoomComponent = new RoomComponent();
	nc.addElement(rc);
	chatRoomNavigator.addChild(nc);
}