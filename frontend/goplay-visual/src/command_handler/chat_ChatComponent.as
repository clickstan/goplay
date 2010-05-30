// ActionScript file

import comm.Conn;

protected static function chatRecievedBroadCast(conn:Conn, trans:int, chat_id:int, sender:String, msg:String):void {
	if ((chat_id in chats) && (chats[chat_id]!=null)) {
		if (sender == null)
			chats[chat_id].conversationTXT.appendText('\n'+msg+"\n" );
		else
			chats[chat_id].conversationTXT.appendText('\n'+sender+" says:"+'\n'+"	"+msg+"\n" );
	}
}