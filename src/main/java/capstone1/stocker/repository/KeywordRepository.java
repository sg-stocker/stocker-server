package capstone1.stocker.repository;

import capstone1.stocker.domain.Company;
import capstone1.stocker.domain.Keyword;
import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface KeywordRepository extends JpaRepository<Keyword, Long> {

    Optional<Keyword> findById(Long keywordId);

    List<Keyword> findAllByCompany(Company company);
}
