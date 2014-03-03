select u.login,d.* from wp_download d, sq_user u where u.id=d.owner_id order by d.id desc
