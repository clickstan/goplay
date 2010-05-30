import flash.utils.Dictionary;

import mx.controls.Image;

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

public static function xyToGoNotation(x:int, y:int):String {
	return xToAlphabet[x] + y;
}

public function makeMove(color:String, move:String):void {
	var stone:Image = stones[move];
	var source:Object = color=="black"? black_source.source : white_source.source;
	stone.source = source;
	
	// TODO: ver si se capturan piezas
	trace("TODO: board.as makeMove");
}