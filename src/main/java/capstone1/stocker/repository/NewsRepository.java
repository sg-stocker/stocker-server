package capstone1.stocker.repository;

import capstone1.stocker.domain.News;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface NewsRepository extends JpaRepository<News, Long> {

    List<News> findNewsByKeywordId(Long keywordId);

}
