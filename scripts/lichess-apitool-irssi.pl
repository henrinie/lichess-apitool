#!/usr/bin/perl
# This script can be used with irssi to create a bot utilizing lichess-apitool.
# Requires python to be installed, and lichess-apitool.py has to be executable by your irssi user.
use Irssi::Irc;
use threads;

$VERSION = '0.2';
%IRSSI = (
    authors     => 'Henri Nieminen',
    contact     => 'henri.nieminen@gmail.com',
    name        => 'lichess-apitool-irssi',
    description => 'Post information of listed lichess users to a irc channel by utilizing lichess-apitool.',
    license     => 'Public',
    url         => '',
    changed     => $VERSION,
);
### SETTINGS

# Channel to monitor. Eg. "#mychannel"
my $channel = "";
# Irc server to monitor. Eg. "freenode"
my $myserver = "";

# Location of lichess-apitool.py
my $apitool = "/location/to/lichess-apitool/lichess-apitool.py"

### CODE
# Don't edit things below if you don't know what you are doing.


sub message_public{
	my($server, $msg, $nick, $address, $target) = @_;

	if($target eq $channel){
		# If the msg begins with '.' (a dot), run a method that runs the command, if it is one
		if ($msg =~ /^\.(\w+)/) {
			# Get rid of the dot from $msg before doing commandlist()
			$msg =~ s/^\.//;
			sendcommand($server, $target, $msg);
		}
	}
}


sub sendcommand {
	my ($server, $target, $msg) = @_;
	my $sendmsg = "";

	($sendmsg) = `python $apitool $msg`;
	
	if ($sendmsg eq "") {
		# Do nothing
	}
	elsif ($sendmsg =~ /^Error:/) {
		print ( CRAP $sendmsg );
	}
	else {
		threads->create(\&send_to_channel, $server, $target, $sendmsg);
	}
}


sub send_to_channel {
        my ($server, $target, $msg) = @_;
        $server->command("MSG ". $target ." ".$msg);
}

Irssi::signal_add("message public", "message_public");