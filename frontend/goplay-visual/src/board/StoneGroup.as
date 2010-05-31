package board
{
	import mx.controls.Image;

	public class StoneGroup
	{
		public var id:int;
		public var stones:Array = new Array();	// array of stones data
		
		public function StoneGroup()
		{
			id = nextGroupId();
		}
		
		public function add(sd:StoneData):void {
			if (!(sd in stones)) {
				stones.push(sd);
			}
		}
		
		public function size():int {
			return stones.length;
		}
		
		private static var _groupid:int = 0;
		private static function nextGroupId():int {
			return _groupid++;
		}
	}
}