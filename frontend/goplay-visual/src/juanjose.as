import flash.utils.Dictionary;

import spark.components.HGroup;

public function tabNavigatorCreated():void {
	createRoomNavigatorContent("main");
}

public function createRoomBtn():void {
	if (createRoomB.label != "OK") {
		createRoomTxt.visible = true;
		createRoomB.label = "OK"
	} else {
		trace("sending createRoom command name=",createRoomTxt.text);
		var obj:Object = Room.createRoom(createRoomTxt.text);
		conn.send(obj);
		
		createRoomB.label = "Create"
		createRoomTxt.visible = false;
		createRoomTxt.text = "new room"
	}
} 



public function openRoom():void {
	var name:String = roomsGrid.selectedItem.toString();
	var openedNV:Object = chatRoomNavigator.getChildByName(name);
	if (openedNV == null) {
		trace("sending openRoom(",name,")");
		var obj:Object = Room.openRoom(name);
		conn.addResponseHandler(createRoomNavigatorContentCaller, obj.trans);
		conn.send(obj);
	}
}

public function createRoomNavigatorContentCaller(obj:Object):void {
	createRoomNavigatorContent(obj.name);
}

public function createRoomNavigatorContent(name:String):void {
	var openedNV:Object = chatRoomNavigator.getChildByName(name);
	if (openedNV == null) {
		var nc:NavigatorContent = new NavigatorContent();
		nc.name = name;
		nc.label = name;
		var rc:RoomComponent = new RoomComponent();
		rc.init(name);
		nc.addElement(rc);
		chatRoomNavigator.addChild(nc);
	}
}


public function createRoomNavigatorContent_ChatOnly(name:String, chat_id:int):void {
	var nc:NavigatorContent = new NavigatorContent();
	nc.name = name;
	nc.label = name;
	var cc:ChatComponent = new ChatComponent();
	cc.init(chat_id);
	nc.addElement(cc);
	chatRoomNavigator.addChild(nc);
}

public function createRoomNavigatorContent_Game(name:String, game_id:int, chat_id:int,
												black:String, white:String, size:int, komi:Number, handicap:int,
												timed_game:Boolean, main_time:int, byo_yomi:Number,
												moves_handicap:Array, moves_all:Array, resigned:String, score:String):void
{
	var nc:NavigatorContent = new NavigatorContent();
	nc.name = name;
	nc.label = name;
	
	var cc:ChatComponent = new ChatComponent();
	cc.init(chat_id, true);
	
	var container:HGroup = new HGroup();
	container.requestedColumnCount = 2;
	container.variableColumnWidth=true;
	container.width = chatRoomNavigator.width;
	container.height = chatRoomNavigator.height;
	
	nc.addElement(container);
	
	var bc9:BoardComponent9;
	var bc13:BoardComponent13;
	var bc19:BoardComponent;
	
	switch (size) {
		case 9:
			bc9 = new BoardComponent9();
			bc9.init(game_id, chat_id,
					 black, white, size, komi, handicap,
					 timed_game, main_time, byo_yomi,
					 moves_handicap, moves_all, resigned, score);
			container.addElement(bc9);
			break;
		case 13:
			bc13 = new BoardComponent13();
			//bc13.init(game_id);
			container.addElement(bc19);
			break;
		case 19:
			bc19 = new BoardComponent();
			//bc19.init(game_id);
			container.addElement(bc19);
			break;
	}
	
	container.addElement(cc);
	chatRoomNavigator.addChild(nc);
}
