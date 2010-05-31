import board.StoneData;
import board.StoneGroup;

import comm.Conn;
import comm.protocol.ClientProtocol;
import comm.protocol.server.Game;

import flash.geom.Point;
import flash.utils.Dictionary;

public static var xToAlphabet:Dictionary = new Dictionary();
xToAlphabet[1] = "A";
xToAlphabet[2] = "B";
xToAlphabet[3] = "C";
xToAlphabet[4] = "D";
xToAlphabet[5] = "E";
xToAlphabet[6] = "F";
xToAlphabet[7] = "G";
xToAlphabet[8] = "H";
xToAlphabet[9] = "J";
xToAlphabet[10] = "K";
xToAlphabet[11] = "L";
xToAlphabet[12] = "M";
xToAlphabet[13] = "N";
xToAlphabet[14] = "O";
xToAlphabet[15] = "P";
xToAlphabet[16] = "Q";
xToAlphabet[17] = "R";
xToAlphabet[18] = "S";
xToAlphabet[19] = "T";

public static var alphabetToX:Dictionary = new Dictionary();
alphabetToX["A"] = 1;
alphabetToX["B"] = 2;
alphabetToX["C"] = 3;
alphabetToX["D"] = 4;
alphabetToX["E"] = 5;
alphabetToX["F"] = 6;
alphabetToX["G"] = 7;
alphabetToX["H"] = 8;
alphabetToX["J"] = 9;
alphabetToX["K"] = 10;
alphabetToX["L"] = 11;
alphabetToX["M"] = 12;
alphabetToX["N"] = 13;
alphabetToX["O"] = 14;
alphabetToX["P"] = 15;
alphabetToX["Q"] = 16;
alphabetToX["R"] = 17;
alphabetToX["S"] = 18;
alphabetToX["T"] = 19;

public var game_id:int;
public var chat_id:int;
public var black:String;
public var white:String;
public var size:int;
public var komi:Number;
public var handicap:int;
public var timed_game:Boolean;
public var main_time:int;
public var byo_yomi:Number;
public var moves_handicap:Array;
public var moves_all:Array;
public var resigned:String;
public var score:String;

public var player_color:String;

// maps for example: "A1" -> StoneData
private var stones:Dictionary = new Dictionary();

public function init(game_id:int, chat_id:int,
					 black:String, white:String, size:int, komi:Number, handicap:int,
					 timed_game:Boolean, main_time:int, byo_yomi:Number,
					 moves_handicap:Array, moves_all:Array, resigned:String, score:String):void
{
	Main.games[game_id] = this;
	
	this.game_id = game_id;
	this.chat_id = game_id;
	this.black = black;
	this.white = white;
	this.size = size;
	this.komi = komi;
	this.handicap = handicap;
	this.timed_game = timed_game;
	this.main_time = main_time;
	this.byo_yomi = byo_yomi;
	this.moves_handicap = moves_handicap;
	this.moves_all = moves_all;
	this.resigned = resigned;
	this.score = score;
	
	if (black == Main.currentUser)
		player_color = black;
	else if (white == Main.currentUser)
		player_color = white;
	else
		player_color = null;
}

public static function xyToGoNotation(x:int, y:int):String {
	return xToAlphabet[x] + y;
}

public static function goNotationToXY(pos:String):Point {
	return new Point(alphabetToX[pos.charAt(0)], int(pos.slice(1)));
}

public function makeMove(color:String, move:String):void {
	var sd:StoneData = stones[move];
	var source:Object = color=="black"? black_source.source : white_source.source;
	
	sd.image.source = source;
	
	var friends_surrounding:Array = getStonesSurrounding(color, move, isFriend);
	var enemies_surrounding:Array = getStonesSurrounding(color, move, isEnemy);
	
	// set groups
	
	if (friends_surrounding.length == 0) 
		// new group
		sd.newGroup();
	else if (friends_surrounding.length == 1)
		// join to group
		friends_surrounding[0].addToGroup(sd);
	else {
		// join groups
		trace("makeMove -  join groups:", friends_surrounding);
		sd.joinGroups(friends_surrounding);
	}
	
	// captures
	// ..
}


public function isEnemy(color:String, sd:StoneData):Boolean {
	if (color == "black")
		return isWhite(sd);
	else
		return isBlack(sd);
}

public function isFriend(color:String, sd:StoneData):Boolean {
	if (color == "white")
		return isWhite(sd);
	else
		return isBlack(sd);
}

public function isBlack(sd:StoneData):Boolean {
	return sd.image.source == black_source.source
}

public function isWhite(sd:StoneData):Boolean {
	return sd.image.source == white_source.source
}

public function isTransparent(sd:StoneData):Boolean {
	return sd.image.source == transparent_source.source
}

/* returns an array of stones data, corresponding to the stones surrounding the stone
 * in position "pos" only if the 'test' function returns true for that stone
 */
private function getStonesSurrounding(color:String, pos:String, test:Function):Array {
	var p:Point = goNotationToXY(pos);
	var stones_s:Array = new Array();
	
	function testAndPush(_pos:String):void {
		var sd:StoneData = stones[_pos]
		if ((sd != null) && test(color, sd))
			stones_s.push(sd);
	}
	
	testAndPush(xyToGoNotation(p.x, p.y+1));
	testAndPush(xyToGoNotation(p.x, p.y-1));
	testAndPush(xyToGoNotation(p.x-1, p.y));
	testAndPush(xyToGoNotation(p.x+1, p.y));
	
	return stones_s;
}
