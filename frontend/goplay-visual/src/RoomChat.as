// ActionScript file
protected function chat_creationCompleteHandler(event:FlexEvent):void
{
	var obj:Object = Room.getChatId(roomname);
	Main.conn.addResponseHandler(initializeChatId, obj.trans);
	Main.conn.send(obj);
}
protected function initializeChatId(object:Object):void {
	chatid = object.id;
	chatComponent.init(chatid);
}