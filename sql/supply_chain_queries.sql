SELECT SKU_ID, SUM(Units_Sold) AS total_sold FROM supply_chain.inventory GROUP BY SKU_ID ORDER BY total_sold DESC LIMIT 10;

SELECT Supplier_ID, AVG(Supplier_Lead_Time_Days) AS avg_lead FROM supply_chain.inventory GROUP BY Supplier_ID ORDER BY avg_lead DESC;

SELECT SKU_ID, COUNT(*) AS low_days FROM supply_chain.inventory WHERE Inventory_Level < Reorder_Point GROUP BY SKU_ID ORDER BY low_days DESC LIMIT 10;

SELECT Warehouse_ID, SUM(Inventory_Level * Unit_Cost) AS inv_value FROM supply_chain.inventory GROUP BY Warehouse_ID ORDER BY inv_value DESC;

SELECT Region, SUM(Units_Sold) AS actual, SUM(Demand_Forecast) AS forecast FROM supply_chain.inventory GROUP BY Region;