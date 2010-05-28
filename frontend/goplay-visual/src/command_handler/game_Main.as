// ActionScript file

import comm.Conn;

import notify.Notification;

public function gameCHandler_callInto(conn:Conn, trans:int, game_id:int, sender:String):void {
	var options:Array = new Array();
	
	var notification:Notification = new Notification(sender + " has challenged you", options);
	
	options.push({'label':'accept',
		'handler':{'func':gameCCallback_callInto_accept,
			'args':new Array(conn, trans, game_id, notification)}});
	
	options.push({'label':'reject',
		'handler':{'func':gameCCallback_callInto_reject,
			'args':new Array(conn, trans, notification)}});
	
	notify_control.addNotification(notification);
}

private function gameCCallback_callInto_accept(conn:Conn, trans:int, game_id:int, notification:Notification):void {
	conn.send({'trans':trans, 'accepted':true});
	notify_control.removeNotification(notification);
	
	// TODO: crear tab de game con game_id = game_id
	trace('gameCCallback_callInto_accept', 'ready to play in game_id', game_id)
}

private function gameCCallback_callInto_reject(conn:Conn, trans:int, notification:Notification):void {
	conn.send({'trans':trans, 'accepted':false});
	notify_control.removeNotification(notification);
}