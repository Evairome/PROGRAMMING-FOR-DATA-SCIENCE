USE `pollution-db2`;
SELECT 
    `Date_Time`, 
    Location, 
    NOx 
FROM reading 
INNER JOIN site ON 
    site.SiteID = reading.SiteID 
WHERE 
    YEAR(Date_Time) = 2019 
ORDER BY 
    NOx DESC LIMIT 1;
