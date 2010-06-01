// ActionScript file

import comm.Conn;

public static function roomCHandler_adduser(conn:Conn, trans:int, roomname:String, username:String):void {
	trace("room_chandler_adduser", roomname, username);
	rooms[roomname].addPlayer(username);
}

public static function roomCHandler_removeuser(conn:Conn, trans:int, roomname:String, username:String):void {
	trace("room_chandler_removeuser", roomname, username);
	rooms[roomname].removePlayer(username);
}