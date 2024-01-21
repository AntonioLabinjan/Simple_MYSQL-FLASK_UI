CREATE DATABASE IF NOT EXISTS proizvodi;
USE proizvodi;

CREATE TABLE IF NOT EXISTS proizvod (
    id INT AUTO_INCREMENT PRIMARY KEY,
    naziv VARCHAR(255) NOT NULL UNIQUE,
    cijena DECIMAL(10, 2) NOT NULL
);

SELECT SUM(cijena) AS ukupna_cijena_proizvoda FROM proizvod ;



DELIMITER //


CREATE PROCEDURE smanji_cijene_proizvoda(IN p_proizvod_id INT, IN p_popust DECIMAL(5, 2))
BEGIN
    DECLARE stara_cijena DECIMAL(10, 2);
	DECLARE iznos_smanjenja DECIMAL(10, 2);
    -- Dohvati trenutnu cijenu proizvoda
    SELECT cijena INTO stara_cijena FROM proizvod WHERE id = p_proizvod_id;

    -- Ako je proizvod pronađen, ažuriraj cijenu s popustom
        SET iznos_smanjenja = stara_cijena * (p_popust / 100);

        UPDATE proizvod SET cijena = stara_cijena - iznos_smanjenja WHERE id = p_proizvod_id;
        SELECT CONCAT('Cijena proizvoda smanjena za ', p_popust, '%.') AS poruka;
END //

DELIMITER ;


SELECT * FROM proizvod;

CALL smanji_cijenu_proizvoda (5, 50);

SELECT CONCAT('Svi uneseni proizvodi su: ', GROUP_CONCAT(CONCAT(naziv, ' sa cijenom od: ', cijena) SEPARATOR '; ')) AS rezultat
FROM proizvod;
