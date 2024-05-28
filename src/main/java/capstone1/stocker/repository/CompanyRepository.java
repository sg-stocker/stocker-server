package capstone1.stocker.repository;

import capstone1.stocker.domain.Company;
import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CompanyRepository extends JpaRepository<Company, Long> {

    List<Company> findAll();

    boolean existsByTicker(String ticker);

    Optional<Company> findByTicker(String ticker);
}
