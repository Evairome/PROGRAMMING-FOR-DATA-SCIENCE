USE `pollution-db2`;
SELECT 
    SiteID, 
    AVG(`PM2.5`) `Avg_PM2.5`, 
    AVG(`VPM2.5`) `Avg vpm2.5` 
FROM 
    reading 
WHERE 
    (YEAR(Date_Time) BETWEEN 2010 AND 2019) AND -- Values Near 8:00 include values between 7:45 - 8:15
    ((MINUTE(Date_Time) BETWEEN 45 AND 59 AND HOUR(Date_Time) = 7) 
    OR (MINUTE(Date_Time) BETWEEN 0 AND 15 AND HOUR(Date_Time) = 8)) 
GROUP BY SiteID AND YEAR(Date_Time);