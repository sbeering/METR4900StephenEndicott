#Select the correctly time formatted data based on a MAC Address
SELECT FROM_UNIXTIME(CONVERT(`found_devices`.`time`, DECIMAL),'%Y %D %M %h:%i:%s %x') AS `goodTime` 
FROM `found_devices`
WHERE `MAC_address` = '5c:0a:5b:1f:64:bc'



#Select the correctly time formatted data and location based on a MAC Address
SELECT `found_devices`.`MAC_address` ,FROM_UNIXTIME(CONVERT(`found_devices`.`time`, DECIMAL),'%D %M %Y %h:%i:%s %x') AS `time`, `stations`.`location`
FROM `found_devices`
INNER JOIN `found_devices`.`stations_id` = `stations`.`station_id`
WHERE `MAC_address` =  `5c:0a:5b:1f:64:bc`;


#Select the correctly time formatted data and location based on a MAC Address
SELECT `found_devices`.`MAC_address` ,FROM_UNIXTIME(CONVERT(`found_devices`.`time`, DECIMAL),'%D %M %Y %k:%i:%s') AS `time`,`stations`.`location`
FROM `found_devices`
INNER JOIN `stations` ON `found_devices`.`stations_id` = `stations`.`station_id`
WHERE `found_devices`.`MAC_address` =  '00:80:92:4b:27:7a'


#Select the cop pinging MAC_addresses from the database
SELECT COUNT(`MAC_address`) AS count, `MAC_address` 
FROM `found_devices`
GROUP BY `MAC_address`
ORDER BY count DESC
LIMIT 20;