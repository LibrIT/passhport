#! /usr/bin/perl
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>. 
use strict;
use warnings;
use Data::Dumper;
use REST::Client;

my $bash_output=1;

# This pointer will contains all passhportd configuration
my $passhport_conf;

###################
# First we get target infos
my $targets_infos;
my $targets_list = &get_targets_list;

foreach my $targetname (@$targets_list){
	$targets_infos = &get_target_infos($targetname, $targets_infos);
}

$passhport_conf->{targets_infos} = $targets_infos ;

###################
# We get the targetgroup infos
my $targetgroups_infos;
my $targetgroups_list = &get_targetgroups_list;

foreach my $targetgroupname (@$targetgroups_list){
	$targetgroups_infos = &get_targetgroup_infos($targetgroupname, $targetgroups_infos);
}

$passhport_conf->{targetgroups_infos} = $targetgroups_infos ;

###################
# We get the user infos
my $users_infos;
my $users_list = &get_users_list;

foreach my $username (@$users_list){
	$users_infos = &get_user_infos($username, $users_infos);
}

$passhport_conf->{users_infos} = $users_infos ;

###################
# We get the usergroup infos
my $usergroups_infos;
my $usergroups_list = &get_usergroups_list;

foreach my $usergroupname (@$usergroups_list){
	$usergroups_infos = &get_usergroup_infos($usergroupname, $usergroups_infos);
}

$passhport_conf->{usergroups_infos} = $usergroups_infos ;



###################
# We output commands to restore config :
&generate_target_restore_commands($passhport_conf) if ( $bash_output );
&generate_targetgroup_restore_commands($passhport_conf) if ( $bash_output );
&generate_user_restore_commands($passhport_conf) if ( $bash_output );
&generate_usergroup_restore_commands($passhport_conf) if ( $bash_output );
&generate_populate_targetgroup($passhport_conf) if ( $bash_output );
&generate_populate_usergroup($passhport_conf) if ( $bash_output );



##############
# TARGETS SUBs
##############
sub get_targets_list{
	my $targets_list_rest = REST::Client->new();
	$targets_list_rest->GET('https://passhportd.librit.fr/target/list');
	my @targets_list = split /\n/, $targets_list_rest->responseContent();
	return \@targets_list;
}

sub get_target_infos {
	my $targetname = shift @_;
	my $targets_infos = shift @_;
	my $target_info_rest = REST::Client->new();
	$target_info_rest->GET("https://passhportd.librit.fr/target/show/$targetname");
	my @target_infos = split /\n/, $target_info_rest->responseContent();
	foreach my $targetinfo (@target_infos){
		$targetinfo =~ /^([^:]+):\s*(.*)$/;
		my ($param_name, $param_value) = ($1, $2);

		$targets_infos->{$targetname}->{$param_name} = $param_value;

	}
	return $targets_infos;
}

sub generate_target_restore_commands{
	my $passhport_conf = shift @_;
	my $targets_infos = $passhport_conf->{'targets_infos'};
	foreach my $target_name (keys(%$targets_infos))
	{
		print "passhport-admin target create $target_name " . $targets_infos->{$target_name}->{Hostname};
		print " --login=\"" . $targets_infos->{$target_name}->{Login} . "\"";
		print " --port=\"" . $targets_infos->{$target_name}->{Port} . "\"";
		print " --comment=\"" . $targets_infos->{$target_name}->{Comment} . "\"";
		print " --sshoptions=\"" . $targets_infos->{$target_name}->{'SSH options'} . "\"";
		print "\n";
	}
}

##############
# USERS SUBs
##############
sub get_users_list{
	my $users_list_rest = REST::Client->new();
	$users_list_rest->GET('https://passhportd.librit.fr/user/list');
	my @users_list = split /\n/, $users_list_rest->responseContent();
	return \@users_list;
}

sub get_user_infos {
	my $username = shift @_;
	my $users_infos = shift @_;
	my $user_info_rest = REST::Client->new();
	$user_info_rest->GET("https://passhportd.librit.fr/user/show/$username");
	my @user_infos = split /\n/, $user_info_rest->responseContent();
	foreach my $userinfo (@user_infos){
		$userinfo =~ /^([^:]+):\s*(.*)$/;
		my ($param_name, $param_value) = ($1, $2);

		$users_infos->{$username}->{$param_name} = $param_value;

	}
	return $users_infos;
}

sub generate_user_restore_commands{
	my $passhport_conf = shift @_;
	my $users_infos = $passhport_conf->{'users_infos'};
	foreach my $user_name (keys(%$users_infos))
	{
		print "passhport-admin user create $user_name '" . $users_infos->{$user_name}->{'SSH key'} . "'\n";
	}
}

##############
# TARGETGROUP SUBs
##############
sub get_targetgroups_list{
	my $targetgroups_list_rest = REST::Client->new();
	$targetgroups_list_rest->GET('https://passhportd.librit.fr/targetgroup/list');
	my @targetgroups_list = split /\n/, $targetgroups_list_rest->responseContent();
	return \@targetgroups_list;
}

sub get_targetgroup_infos {
	my $targetgroupname = shift @_;
	my $targetgroups_infos = shift @_;
	my $targetgroup_info_rest = REST::Client->new();
	$targetgroup_info_rest->GET("https://passhportd.librit.fr/targetgroup/show/$targetgroupname");
	my @targetgroup_infos = split /\n/, $targetgroup_info_rest->responseContent();
	foreach my $targetgroupinfo (@targetgroup_infos){
		$targetgroupinfo =~ /^([^:]+):\s*(.*)$/;
		my ($param_name, $param_value) = ($1, $2);

		$targetgroups_infos->{$targetgroupname}->{$param_name} = $param_value;

	}
	return $targetgroups_infos;
}

sub generate_targetgroup_restore_commands{
	my $passhport_conf = shift @_;
	my $targetgroups_infos = $passhport_conf->{'targetgroups_infos'};
	foreach my $targetgroup_name (keys(%$targetgroups_infos))
	{
		print "passhport-admin targetgroup create \"$targetgroup_name\" ";
		print " --comment=\"" . $targetgroups_infos->{$targetgroup_name}->{Comment} . "\"";
		print "\n";
	}
}

sub generate_populate_targetgroup{
	my $passhport_conf = shift @_;
	my $targetgroups_infos = $passhport_conf->{'targetgroups_infos'};
	foreach my $targetgroup_name (keys(%$targetgroups_infos))
	{
		foreach my $target (split / /, $targetgroups_infos->{$targetgroup_name}->{'Target list'})
		{
			print "passhport-admin targetgroup addtarget \"$target\" \"$targetgroup_name\"\n";
		}
		foreach my $targetgroup (split / /, $targetgroups_infos->{$targetgroup_name}->{'Targetgroup list'})
		{
			print "passhport-admin targetgroup addtargetgroup \"$targetgroup\" \"$targetgroup_name\"\n";
		}
		foreach my $usergroup (split / /, $targetgroups_infos->{$targetgroup_name}->{'Usergroup list'})
		{
			print "passhport-admin targetgroup addusergroup \"$usergroup\" \"$targetgroup_name\"\n";
		}
		foreach my $user (split / /, $targetgroups_infos->{$targetgroup_name}->{'User list'})
		{
			print "passhport-admin targetgroup adduser \"$user\" \"$targetgroup_name\"\n";
		}
	}
}

##############
# USERGROUP SUBs
##############
sub get_usergroups_list{
	my $usergroups_list_rest = REST::Client->new();
	$usergroups_list_rest->GET('https://passhportd.librit.fr/usergroup/list');
	my @usergroups_list = split /\n/, $usergroups_list_rest->responseContent();
	return \@usergroups_list;
}

sub get_usergroup_infos {
	my $usergroupname = shift @_;
	my $usergroups_infos = shift @_;
	my $usergroup_info_rest = REST::Client->new();
	$usergroup_info_rest->GET("https://passhportd.librit.fr/usergroup/show/$usergroupname");
	my @usergroup_infos = split /\n/, $usergroup_info_rest->responseContent();
	foreach my $usergroupinfo (@usergroup_infos){
		$usergroupinfo =~ /^([^:]+):\s*(.*)$/;
		my ($param_name, $param_value) = ($1, $2);

		$usergroups_infos->{$usergroupname}->{$param_name} = $param_value;

	}
	return $usergroups_infos;
}

sub generate_usergroup_restore_commands{
	my $passhport_conf = shift @_;
	my $usergroups_infos = $passhport_conf->{'usergroups_infos'};
	foreach my $usergroup_name (keys(%$usergroups_infos))
	{
		print "passhport-admin usergroup create \"$usergroup_name\"";
		print " --comment=\"" . $usergroups_infos->{$usergroup_name}->{Comment} . "\"";
		print "\n";
	}
}

sub generate_populate_usergroup{
	my $passhport_conf = shift @_;
	my $usergroups_infos = $passhport_conf->{'usergroups_infos'};
	foreach my $usergroup_name (keys(%$usergroups_infos))
	{
		foreach my $usergroup (split / /, $usergroups_infos->{$usergroup_name}->{'Usergroup list'})
		{
			print "passhport-admin usergroup addusergroup \"$usergroup\" \"$usergroup_name\"\n";
		}
		foreach my $user (split / /, $usergroups_infos->{$usergroup_name}->{'User list'})
		{
			print "passhport-admin usergroup adduser \"$user\" \"$usergroup_name\"\n";
		}
	}
}
