def search_cond(condition, price_low, price_high): #called in views.search
    cmd = f'''
    SELECT p.name prod_name, 
        (SELECT d.name
        FROM drug.drug d
        WHERE d.id = p.drug_id) drug_name,
        p.avg_price
    FROM drug.product p
    WHERE p.source_id = 1 #wiki
    AND p.drug_id IN (SELECT t.drug_id
                    FROM drug.treatment t
                    WHERE t.source_id = 1 #wiki
                    AND t.condition_id IN (SELECT c.id
                                            FROM drug.condition c
                                            WHERE c.name = "{condition}"
                                            AND c.source_id = 1 #wiki
                        )
                    )
    AND p.avg_price < {price_high}
    AND p.avg_price >= {price_low}
    ORDER BY p.avg_price
    '''
    return cmd

def search_cond_currmed(condition, price_low, price_high, current_med):
    cmd = f'''
    WITH curr_med_d AS (SELECT p.drug_id
                        FROM drug.product p
                        WHERE p.name = "{current_med}"
                        AND p.source_id = 1 #wiki
                        )
    SELECT p.name prod_name, 
        (SELECT d.name
        FROM drug.drug d
        WHERE d.id = p.drug_id) drug_name,
        p.avg_price
    FROM drug.product p 
    WHERE p.source_id = 1 #wiki
    AND p.avg_price < {price_high}
    AND p.avg_price >= {price_low}
    AND EXISTS (SELECT 1
                FROM drug.treatment t
                WHERE t.source_id = 1 #wiki
                and t.drug_id = p.drug_id
                #Treatment treats condition
                AND EXISTS (SELECT 1
                            FROM drug.condition c
                            WHERE c.name = "{condition}"
                            AND c.source_id = 1 #wiki
                            AND t.condition_id = c.id
                            )
                #Treatment doesn't interact with current med
                AND NOT EXISTS (SELECT 1
                                FROM drug.interaction i
                                WHERE i.source_drug_id = t.drug_id
                                AND i.target_drug_id IN (SELECT drug_id
                                                        FROM curr_med_d cmd
                                    )
                            )
    )
    '''
    return cmd

def search_prod_prices(source_id, prod_name): #called in views.prod_page
    cmd = f'''
    SELECT
        (SELECT s.name
        FROM drug.store s
        WHERE pr.store_id = s.id
        ) Store,
        CASE WHEN pr.type != "COUPON" THEN "MEMBER"
            ELSE pr.type
            END Type,
        ROUND(pr.price, 2) Price,
        pr.url Link
    FROM drug.price pr 
    WHERE pr.url != ''
    AND EXISTS (SELECT 1
                FROM drug.product p
                WHERE pr.product_id = p.id
                AND p.source_id = {source_id}
                AND p.name = "{prod_name}"
                )
    ORDER by pr.price 
    '''
    return cmd


#pr.type Type,

def search_drug_prods(source_id, drug_name): #called in views.drug_page
    cmd = f'''
    SELECT p.name,
        p.avg_price
    FROM drug.product p
    WHERE p.source_id = {source_id} #wiki
    AND EXISTS (SELECT 1
                FROM drug.drug d
                WHERE d.id = p.drug_id
                AND d.name = "{drug_name}")
    ORDER by p.name 
    '''
    return cmd

def search_drug_tmt(source_id, drug_name): #called in views.drug_page
    cmd = f'''
    SELECT c.name,
        c.url
    FROM drug.condition c
    WHERE c.source_id = 2
    AND EXISTS (SELECT 1
                FROM drug.treatment t
                WHERE t.source_id = 2
                AND t.condition_id = c.id
                AND EXISTS (SELECT 1
                            FROM drug.drug d 
                            WHERE t.drug_id = d.id 
                            AND d.name = "{drug_name}"
                    )
                )
    '''
    return cmd