package board
{
	import mx.controls.Image;

	public class StoneData
	{
		public var name:String;
		public var image:Image;
		public var group:StoneGroup;
		
		public function StoneData(name:String, image:Image=null, group:StoneGroup=null)
		{
			this.name = name;
			this.image = image;
			this.group = group;
		}
		
		public function newGroup():void {
			group = new StoneGroup();
			addToGroup(this);
		}
		
		public function addToGroup(sd:StoneData):void {
			group.add(sd);
			sd.group = group;
			sd.image.toolTip = group.id.toString();
		}
		
		public function joinGroups(sds:Array):void {
			newGroup();
			
			var proccesed:Array = new Array();
			
 outerloop: for (var i_sd:int=0; i_sd<sds.length; i_sd++) {
				var sd:StoneData = sds[i_sd];
				for (var j_sd:int=0; j_sd<sd.group.size(); j_sd++) {
					var _sd:StoneData = sd.group.stones[j_sd];
					if (_sd in proccesed) continue outerloop;
					proccesed.push(_sd);
					addToGroup(_sd);
				}
			}
		}
		
		public function toString():String {
			return "SD:"+name;
		}
	}
}