package capstone1.stocker.repository;

import capstone1.stocker.domain.Company;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CompanyRepository extends JpaRepository<Company, Long> {

    List<Company> findAll();
}
