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
}

private function gameCCallback_callInto_reject(conn:Conn, trans:int, notification:Notification):void {
	conn.send({'trans':trans, 'accepted':false});
	notify_control.removeNotification(notification);
}


public function gameCHandler_initialize(conn:Conn, trans:int, game_id:int, chat_id:int,
										black:String, white:String, size:int, komi:Number, handicap:int,
										timed_game:Boolean, main_time:int, byo_yomi:Number,
										moves_handicap:Array, moves_all:Array, resigned:String, score:String):void
{
	var enemy:String = currentUser == black? white : black;
	
	createRoomNavigatorContent_Game("game: "+enemy, game_id, chat_id,
													black, white, size, komi, handicap,
													timed_game, main_time, byo_yomi,
													moves_handicap, moves_all, resigned, score);
}

public static function gameCHandler_play(conn:Conn, trans:int, game_id:int, color:String, move:String):void {
	if ((game_id in Main.games) && (Main.games[game_id] != null))
		Main.games[game_id].makeMove(color, move);
}

public static function gameCHandler_finalScore(conn:Conn, trans:int, game_id:int, score:String):void {
	
	trace("gameCHandler_finalScore", "game_id=", game_id, "score=",score);
	Main.games[game_id].playersInfo.finalScore = score;
}