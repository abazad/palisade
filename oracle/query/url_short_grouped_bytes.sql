Select sum(bytes), req_url_short from sq_access_log_data d
Where d.access_time >= Trunc(Sysdate) and user_name='muminovs'
group by req_url_short
order by 1 desc
