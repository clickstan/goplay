import comm.Conn;

// ActionScript file
protected function chatRecievedBroadCast(conn:Conn, chat_id:int, sender:String, msg:String):void {
	
	trace("chat broadcast recieved from ",sender," msg = ",msg);
	
	for (var i:String in rooms) {
		if (rooms[i].chatid == chat_id) {
			rooms[i].chatComponent.conversationTXT.appendText('\n'+ 
			sender+" says:"+'\n'+"	"+msg+"\n" );

		}
	}
	
}