-- daily_trip_volume
SELECT trip_date, COUNT(*) AS trip_count, ROUND(SUM(total_fare), 2) AS daily_revenue
        FROM transport_trips
        GROUP BY trip_date
        ORDER BY trip_date;

-- avg_fare_by_zone
SELECT zone,
               ROUND(AVG(total_fare), 2) AS avg_fare,
               ROUND(AVG(trip_distance_km), 2) AS avg_distance_km,
               COUNT(*) AS trips
        FROM transport_trips
        GROUP BY zone
        ORDER BY avg_fare DESC;

-- delay_rate_by_traffic
SELECT traffic_level,
               ROUND(AVG(is_delayed), 3) AS delay_rate,
               ROUND(AVG(delay_minutes), 2) AS avg_delay_min,
               COUNT(*) AS trips
        FROM transport_trips
        GROUP BY traffic_level
        ORDER BY delay_rate DESC;

-- revenue_by_vehicle_type
SELECT vehicle_type,
               COUNT(*) AS trips,
               ROUND(SUM(total_fare), 2) AS total_revenue,
               ROUND(AVG(total_fare), 2) AS avg_fare
        FROM transport_trips
        GROUP BY vehicle_type
        ORDER BY total_revenue DESC;

-- peak_hour_analysis
SELECT pickup_hour,
               COUNT(*) AS trips,
               ROUND(AVG(total_fare), 2) AS avg_fare,
               ROUND(AVG(is_delayed), 3) AS delay_rate
        FROM transport_trips
        GROUP BY pickup_hour
        ORDER BY pickup_hour;

-- weather_impact
SELECT weather,
               COUNT(*) AS trips,
               ROUND(AVG(delay_minutes), 2) AS avg_delay_min,
               ROUND(AVG(is_delayed), 3) AS delay_rate
        FROM transport_trips
        GROUP BY weather
        ORDER BY delay_rate DESC;
