// ActionScript file

import comm.Conn;

import notify.Notification;

public function chatCHandler_callInto(conn:Conn, trans:int, chat_id:int, sender:String):void {
	var options:Array = new Array();
	
	var notification:Notification = new Notification(sender + " wants to chat with you", options);
	
	options.push({'label':'accept',
				  'handler':{'func':chatCCallback_callInto_accept,
					  		 'args':new Array(conn, trans, chat_id, notification)}});
	
	options.push({'label':'reject',
				  'handler':{'func':chatCCallback_callInto_reject,
				  			 'args':new Array(conn, trans, notification)}});
	
	notify_control.addNotification(notification);
}

private function chatCCallback_callInto_accept(conn:Conn, trans:int, chat_id:int, notification:Notification):void {
	conn.send({'trans':trans, 'accepted':true});
	trace("accepted chat", chat_id, "trans " + trans)
	notify_control.removeNotification(notification);
}

private function chatCCallback_callInto_reject(conn:Conn, trans:int, notification:Notification):void {
	conn.send({'trans':trans, 'accepted':false});
	trace("rejected chat with trans " + trans);
	notify_control.removeNotification(notification);
}