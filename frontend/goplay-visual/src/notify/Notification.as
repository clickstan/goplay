package notify
{
	import flash.utils.Dictionary;

	public class Notification
	{
		/*
		* options is an array of objects with the form {'label':String, 'handler':Object}
		* where label is the label of the button
		* and handler is an object with the form {'func':Function, 'args':[...]}
		*/
		private var msg:String;
		private var options:Array;
		private var used:Boolean;
		
		public function Notification(msg:String, options:Array=null) {
			this.msg=msg;
			this.options=options;
			this.used=false;
		}
		
		public function getMsg():String {
			return msg;
		}
		
		public function getOptionsLabels():Array {
			var result:Array = new Array();
			for each (var option:Object in options) {
				result.push(option.label)
			}
			return result;
		}
		
		public function getOptions():Array {
			return new Array(options);
		}
		
		public function is_used():Boolean {
			return used;
		}
		
		public function callHandlerByLabel(label:String):void {
			if (used) return;
			for each (var option:Object in options) {
				if (option.label == label) {
					var f:Function = option.handler.func;
					f.apply(null, option.handler.args);
					used = true;
					return
				}
			}
		}
	}
}