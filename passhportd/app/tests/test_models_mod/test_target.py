# -*-coding:Utf-8 -*-
import os

from nose.tools import *
from sqlalchemy import exc

from app import app, db, models
from app.models_mod import user, target, usergroup
from config import basedir


class TestTarget:
    """Test for the class Target"""
    @classmethod
    def setup_class(cls):
        """Initialize configuration and create an empty database before
        testing
        """
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
            os.path.join(basedir, "test.db")
        cls.app = app.test_client()
        db.create_all()

    @classmethod
    def teardown_class(cls):
        """Delete the database created for testing"""
        db.session.remove()
        db.drop_all()

    def setUp(self):
        """Does nothing"""
        pass

    def tearDown(self):
        """Rollback after raising a database exception for testing"""
        db.session.rollback()
        db.session.query(user.User).delete()
        db.session.query(target.Target).delete()
        db.session.query(usergroup.Usergroup).delete()
        db.session.query(models.Target_User).delete()
        db.session.query(models.Target_Group).delete()
        db.session.commit()

    def test_create(self):
        """Target creation in database succeeds"""
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"
        output      = """Targetname: clever_server\nHostname: 127.0.0.1\nPort: 54\nSSH options: --zap\nServertype: Bodhi\nAutocommand: ls -lh\nComment: Magnificent target\nUser list:\nrocket@man.net\nUsergroup list:\nChevaliers_du_zodiaque"""

        name = "rocket@man.net"
        sshkey = "railway"
        comment_user = "speedy"
        user_list = []

        usergroupname = "Chevaliers_du_zodiaque"
        comment_usergroup = "Energie_du_cosmos"
        usergroup_list = []

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment_user)
        user_list.append(u)

        ug = usergroup.Usergroup(
             usergroupname=usergroupname,
             comment=comment_usergroup)
        usergroup_list.append(ug)

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment,
            members=user_list,
            gmembers=usergroup_list)
        db.session.add(t)
        db.session.commit()

        t_db = db.session.query(
            target.Target).filter_by(
            targetname="clever_server").first()

        assert_equal(t_db.targetname, targetname)
        assert_equal(t_db.hostname, hostname)
        assert_equal(t_db.port, port)
        assert_equal(t_db.sshoptions, sshoptions)
        assert_equal(t_db.servertype, servertype)
        assert_equal(t_db.autocommand, autocommand)
        assert_equal(t_db.comment, comment)
        assert_equal(repr(t_db), output)

    @raises(exc.IntegrityError)
    def test_create_existing_targetname(self):
        """Target creation in database with an already used
        targetname fails
        """
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"

        name = "rocket@man.net"
        sshkey = "railway"
        comment_user = "speedy"
        user_list = []

        usergroupname = "Chevaliers_du_zodiaque"
        comment_usergroup = "Energie_du_cosmos"
        usergroup_list = []

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment_user)
        user_list.append(u)

        ug = usergroup.Usergroup(
             usergroupname=usergroupname,
             comment=comment_usergroup)
        usergroup_list.append(ug)

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment,
            members=user_list,
            gmembers=usergroup_list)
        db.session.add(t)
        db.session.commit()

        t = target.Target(
            targetname=targetname,
            hostname="a great host",
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment,
            members=user_list,
            gmembers=usergroup_list)
        db.session.add(t)
        db.session.commit()

    # We should test if an empty targetname while creating a target
    # raises an error, but it seems that SQLite doesn't check it
    # def test_create_empty_targetname(self):

    # We should test if an empty hostname while creating a target
    # raises an error, but it seems that SQLite doesn't check it
    # def test_create_empty_targetname(self):

    def test_edit(self):
        """Target edition in database succeeds"""
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"
        new_targetname = "cleverer_super_server"
        new_hostname    = "192.135.23.54"
        new_port        = 80
        new_sshoptions  = "--plop"
        new_servertype  = "Elive"
        new_autocommand = "ls -klarth"
        new_comment     = "Marvellous target"

        name = "rocket@man.net"
        sshkey = "railway"
        comment_user = "speedy"
        name2 = "palette@color.net"
        sshkey2 = "rough tell"
        comment_user2 = "slow"
        user_list = []

        usergroupname = "Chevaliers_du_zodiaque"
        comment_usergroup = "Energie_du_cosmos"
        usergroupname2 = "Chevaliers d'or"
        comment_usergroup2 = "COSMOOOOS"
        usergroup_list = []

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment_user)
        user_list.append(u)

        ug = usergroup.Usergroup(
             usergroupname=usergroupname,
             comment=comment_usergroup)
        usergroup_list.append(ug)

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment,
            members=user_list,
            gmembers=usergroup_list)
        db.session.add(t)
        db.session.commit()

        u = user.User(
            name=name2,
            sshkey=sshkey2,
            comment=comment_user2)
        user_list.append(u)

        ug = usergroup.Usergroup(
            usergroupname=usergroupname2,
            comment=comment_usergroup2)
        usergroup_list.append(ug)

        target_to_edit = db.session.query(
            target.Target).filter_by(
            targetname="clever_server")
        updated_rows = target_to_edit.update(
            {
                "targetname": new_targetname,
                "hostname": new_hostname,
                "port": new_port,
                "sshoptions": new_sshoptions,
                "servertype": new_servertype,
                "autocommand": new_autocommand,
                "comment": new_comment})
        db.session.commit()

        t_edit = db.session.query(
            target.Target).filter_by(
            targetname=new_targetname).first()

        assert_equal(updated_rows, 1)
        assert_equal(t.id, t_edit.id)
        assert_equal(t_edit.targetname, new_targetname)
        assert_equal(t_edit.hostname, new_hostname)
        assert_equal(t_edit.port, new_port)
        assert_equal(t_edit.sshoptions, new_sshoptions)
        assert_equal(t_edit.servertype, new_servertype)
        assert_equal(t_edit.comment, new_comment)

    def test_edit_non_existing_target(self):
        """Target edition of a non existing target in database
        does nothing (but doesn't raise error)
        """
        t = db.session.query(
            target.Target).filter_by(
            targetname="delicious_target")
        updated_rows = t.update(
            {
                "targetname": "awful",
                "hostname": "batmobile",
                "port": 42,
                "sshoptions": "-p",
                "servertype": "Trisquel",
                "autocommand": "apt-get moo",
                "comment": "So d4rk"})

        assert_equal(updated_rows, 0)

        db.session.commit()

    @raises(exc.IntegrityError)
    def test_edit_existing_targetname(self):
        """Target edition with a new targetname already used in
        database fails
        """
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"
        targetname2  = "bad_server"
        hostname2    = "127.0.0.3"
        port2        = 55
        sshoptions2  = "--zapel"
        servertype2  = "Gentoo"
        autocommand2 = "make foo"
        comment2     = "Worse target"

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment)
        t2 = target.Target(
            targetname=targetname2,
            hostname=hostname2,
            port=port2,
            sshoptions=sshoptions2,
            servertype=servertype2,
            autocommand=autocommand2,
            comment=comment2)

        db.session.add(t)
        db.session.commit()
        db.session.add(t2)
        db.session.commit()

        t2 = db.session.query(
             target.Target).filter_by(
             targetname=targetname2)
        updated_rows = t2.update({"targetname": targetname})

        db.session.commit()

    def test_show(self):
        """Target show in database succeeds"""
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment)
        db.session.add(t)
        db.session.commit()

        target_data = target.Target.query.filter_by(
            targetname=targetname).first()

        assert_equal(targetname, target_data.targetname)
        assert_equal(hostname, target_data.hostname)
        assert_equal(port, target_data.port)
        assert_equal(sshoptions, target_data.sshoptions)
        assert_equal(servertype, target_data.servertype)
        assert_equal(autocommand, target_data.autocommand)
        assert_equal(comment, target_data.comment)

    def test_show_non_existing_target(self):
        """Target show a non existing target in database does nothing
        (but doesn't raise error)
        """
        target_data = target.Target.query.filter_by(
            targetname="bull").first()

        assert_is_none(target_data)

    def test_delete(self):
        """Target deletion in database succeeds"""
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment)
        db.session.add(t)
        db.session.commit()

        db.session.delete(t)
        db.session.commit()

        t_db = db.session.query(
            target.Target).filter_by(
            targetname="clever_server").first()

        assert_is_none(t_db)

    @raises(exc.InvalidRequestError)
    def test_delete_non_existing_target(self):
        """Target deletion with a non existing target fails"""
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment)
        db.session.delete(t)
        db.session.commit()

    def test_list_no_targets(self):
        """Target listing with no target in database succeeds"""
        query = db.session.query(
            target.Target.targetname).order_by(
            target.Target.targetname).all()

        assert_equal(query, [])

    def test_list_existing_targets(self):
        """Target listing with existing targets in database succeeds"""
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"
        target_list = []

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment)
        db.session.add(t)
        db.session.commit()

        query = db.session.query(
            target.Target.targetname).order_by(
            target.Target.targetname).all()
        for row in query:
            target_list.append(str(row[0]))

        target_list = "".join(target_list)

        assert_equal(target_list, "clever_server")

    def test_search(self):
        """Target search with targets matching pattern in database
        succeeds
        """
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"
        targetname2  = "bad_server"
        hostname2    = "127.0.0.3"
        port2        = 55
        sshoptions2  = "--zapel"
        servertype2  = "Gentoo"
        autocommand2 = "make foo"
        comment2     = "Worse target"
        res_list     = []

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment)
        t2 = target.Target(
            targetname=targetname2,
            hostname=hostname2,
            port=port2,
            sshoptions=sshoptions2,
            servertype=servertype2,
            autocommand=autocommand2,
            comment=comment2)

        db.session.add(t)
        db.session.add(t2)
        db.session.commit()

        query = db.session.query(
            target.Target.targetname).filter(
            target.Target.targetname.like(
                "%" +
                "clever" +
                "%")).order_by(
                target.Target.targetname).all()

        for row in query:
            res_list.append(str(row[0]))

        res_list = "\n".join(res_list)

        assert_equal(res_list, "clever_server")

    def test_search_empty_pattern(self):
        """Target searching with an empty pattern returning all targets
        in database succeeds"""
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"
        targetname2  = "bad_server"
        hostname2    = "127.0.0.3"
        port2        = 55
        sshoptions2  = "--zapel"
        servertype2  = "Gentoo"
        autocommand2 = "make foo"
        comment2     = "Worse target"
        res_list     = []

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment)
        t2 = target.Target(
            targetname=targetname2,
            hostname=hostname2,
            port=port2,
            sshoptions=sshoptions2,
            servertype=servertype2,
            autocommand=autocommand2,
            comment=comment2)

        db.session.add(t)
        db.session.add(t2)
        db.session.commit()

        query = db.session.query(
            target.Target.targetname).filter(
            target.Target.targetname.like(
                "%" +
                "" +
                "%")).order_by(
                target.Target.targetname).all()

        for row in query:
            res_list.append(str(row[0]))

        res_list = "\n".join(res_list)

        assert_equal(res_list, "bad_server\nclever_server")

    def test_search_no_users_match_pattern(self):
        """Target searching with a pattern that no target match with
        in database returning nothing succeeds
        """
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"
        res_list = []

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment)

        db.session.add(t)
        db.session.commit()

        query = db.session.query(
            target.Target.targetname).filter(
            target.Target.targetname.like(
                "%" +
                "zhu" +
                "%")).order_by(
                target.Target.targetname).all()

        for row in query:
            res_list.append(str(row[0]))

        res_list = "\n".join(res_list)

        assert_equal(res_list, "")

    def test_add_user(self):
        """Target adding a user succeeds"""
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"

        name = "rasta@populos.museum"
        sshkey = "something"
        comment = "seldom"

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment)

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment)

        db.session.add(t)
        db.session.commit()

        t.adduser(u)
        db.session.commit()

        t_db = db.session.query(
            target.Target).filter_by(
            targetname=targetname).first()

        assert_equal(t_db.members, [u])

    def test_add_user_already_in_target(self):
        """Target adding a user already in target does nothing
        (but doesn't raise error)
        """
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"

        name = "rasta@populos.museum"
        sshkey = "something"
        comment = "seldom"

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment)

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment)

        db.session.add(t)
        db.session.commit()

        t.adduser(u)
        db.session.commit()

        t.adduser(u)
        db.session.commit()

        t_db = db.session.query(
            target.Target).filter_by(
            targetname=targetname).first()

        assert_equal(t_db.members, [u])

    def test_remove_user(self):
        """Target removing a user succeeds"""
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"

        name = "rasta@populos.museum"
        sshkey = "something"
        comment = "seldom"

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment)

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment)

        db.session.add(t)
        db.session.commit()

        t.adduser(u)
        db.session.commit()

        t.rmuser(u)
        db.session.commit()

        t_db = db.session.query(
            target.Target).filter_by(
            targetname=targetname).first()

        assert_equal(t_db.members, [])

    def test_remove_user_not_in_target(self):
        """Target removing a user not in target does nothing
        (but doesn't raise error)
        """
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"

        name = "rasta@populos.museum"
        sshkey = "something"
        comment = "seldom"
        name2 = "marsu@pila.mi"
        sshkey2 = "queue"
        comment2 = "yellow"

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment)

        u = user.User(
            name=name,
            sshkey=sshkey,
            comment=comment)

        u2 = user.User(
            name=name2,
            sshkey=sshkey2,
            comment=comment2)

        db.session.add(t)
        db.session.commit()

        t.adduser(u)
        t.adduser(u2)
        db.session.commit()

        t.rmuser(u)
        db.session.commit()

        t.rmuser(u)
        db.session.commit()

        t_db = db.session.query(
            target.Target).filter_by(
            targetname=targetname).first()

        assert_equal(t_db.members, [u2])

    def test_add_usergroup(self):
        """Target adding a usergroup succeeds"""
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"

        usergroupname = "VVVVVV"
        comment_usergroup = "Captain Viridian to the rescue"

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment)

        ug = usergroup.Usergroup(
            usergroupname=usergroupname,
            comment=comment_usergroup)

        db.session.add(t)
        db.session.commit()

        t.addusergroup(ug)
        db.session.commit()

        t_db = db.session.query(
            target.Target).filter_by(
            targetname=targetname).first()

        assert_equal(t_db.gmembers, [ug])

    def test_add_usergroup_already_in_target(self):
        """Target adding a usergroup already in target does nothing
        (but doesn't raise error)
        """
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"

        usergroupname = "VVVVVV"
        comment_usergroup = "Captain Viridian to the rescue"

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment)

        ug = usergroup.Usergroup(
            usergroupname=usergroupname,
            comment=comment_usergroup)

        db.session.add(t)
        db.session.commit()

        t.addusergroup(ug)
        db.session.commit()

        t.addusergroup(ug)
        db.session.commit()

        t_db = db.session.query(
            target.Target).filter_by(
            targetname=targetname).first()

        assert_equal(t_db.gmembers, [ug])

    def test_remove_usergroup(self):
        """Target removing a usergroup succeeds"""
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"

        usergroupname = "VVVVVV"
        comment_usergroup = "Captain Viridian to the rescue"

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment)

        ug = usergroup.Usergroup(
            usergroupname=usergroupname,
            comment=comment_usergroup)

        db.session.add(t)
        db.session.commit()

        t.addusergroup(ug)
        db.session.commit()

        t.rmusergroup(ug)
        db.session.commit()

        t_db = db.session.query(
            target.Target).filter_by(
            targetname=targetname).first()

        assert_equal(t_db.gmembers, [])

    def test_remove_usergroup_not_in_target(self):
        """Target removing a usergroup not in target does nothing
        (but doesn't raise error)
        """
        targetname  = "clever_server"
        hostname    = "127.0.0.1"
        port        = 54
        sshoptions  = "--zap"
        servertype  = "Bodhi"
        autocommand = "ls -lh"
        comment     = "Magnificent target"

        usergroupname = "VVVVVV"
        comment_usergroup = "Captain Viridian to the rescue"
        usergroupname2 = "PPPPPP"
        comment_usergroup2 = "Captain Pamplemousse need rescue"

        t = target.Target(
            targetname=targetname,
            hostname=hostname,
            port=port,
            sshoptions=sshoptions,
            servertype=servertype,
            autocommand=autocommand,
            comment=comment)

        ug = usergroup.Usergroup(
            usergroupname=usergroupname,
            comment=comment_usergroup)

        ug2 = usergroup.Usergroup(
            usergroupname=usergroupname2,
            comment=comment_usergroup2)

        db.session.add(t)
        db.session.commit()

        t.addusergroup(ug)
        db.session.commit()

        t.rmusergroup(ug2)
        db.session.commit()

        t_db = db.session.query(
            target.Target).filter_by(
            targetname=targetname).first()

        assert_equal(t_db.gmembers, [ug])
