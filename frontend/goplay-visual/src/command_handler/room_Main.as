// ActionScript file

import comm.Conn;

public function roomCHandler_created(conn:Conn, trans:int, roomname:String):void {
	trace("room_chandler_created", roomname);
	var rooms:Array = roomsGrid.dataProvider.toArray();
	if (rooms.indexOf(roomname) == -1)
		roomsGrid.dataProvider.addItem(roomname);
}

public function roomCHandler_destroyed(conn:Conn, trans:int, roomname:String):void {
	trace("room_chandler_destroyed", roomname);
	var rooms:Array = roomsGrid.dataProvider.toArray();
	roomsGrid.dataProvider.removeItemAt(rooms.indexOf(roomname));
}
