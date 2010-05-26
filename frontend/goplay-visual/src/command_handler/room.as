// ActionScript file

import comm.Conn;

public function roomCHandler_adduser(conn:Conn, roomname:String, username:String):void {
	trace("room_chandler_adduser", roomname, username);
}

public function roomCHandler_removeuser(conn:Conn, roomname:String, username:String):void {
	trace("room_chandler_removeuser", roomname, username);
}