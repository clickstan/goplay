// ActionScript file

import comm.Conn;

import notify.Notification;

public function chatCHandler_callInto(conn:Conn, trans:int, chat_id:int, sender:String):void {
	var options:Array = new Array();
	
	var notification:Notification = new Notification(sender + " wants to chat with you", options);
	
	options.push({'label':'accept',
				  'handler':{'func':chatCCallback_callInto_accept,
					  		 'args':new Array(conn, trans, chat_id, sender, notification)}});
	
	options.push({'label':'reject',
				  'handler':{'func':chatCCallback_callInto_reject,
				  			 'args':new Array(conn, trans, notification)}});
	
	notify_control.addNotification(notification);
}

private function chatCCallback_callInto_accept(conn:Conn, trans:int, chat_id:int, sender:String, notification:Notification):void {
	conn.send({'trans':trans, 'accepted':true});
	notify_control.removeNotification(notification);
	
	createRoomNavigatorContent_ChatOnly("chat: "+sender, chat_id);
}

private function chatCCallback_callInto_reject(conn:Conn, trans:int, notification:Notification):void {
	conn.send({'trans':trans, 'accepted':false});
	notify_control.removeNotification(notification);
}