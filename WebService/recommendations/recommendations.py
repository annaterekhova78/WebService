# recommendations/recommendations.py
from concurrent import futures
import random
import grpc
from recommendations_pb2 import (
 BookCategory,
 BookRecommendation,
 RecommendationResponse,
)
import recommendations_pb2_grpc
books_by_category = {
 BookCategory.MYSTERY: [
 BookRecommendation(id=1, title="Мальтийский сокол"),
 BookRecommendation(id=2, title="Убийство в Восточном экспрессе"),
 BookRecommendation(id=3, title="Собака Баскервилей"),
 BookRecommendation(id=4, title="Автостопом по галактике"),
 BookRecommendation(id=5, title="Игра Эндера"),
 BookRecommendation(id=6, title="История с кладбищем"),
 BookRecommendation(id=7, title="Голос монстра"),
 BookRecommendation(id=8, title="Жизнь мальчишки"),
 BookRecommendation(id=9, title="Творец Заклинаний"),
 BookRecommendation(id=10, title="Игра ангела"),
 ],
 BookCategory.SCIENCE_FICTION: [
 BookRecommendation(id=11, title="Дюна"),
 BookRecommendation(id=12, title="Двадцать тысяч лье под водой"),
 BookRecommendation(id=13, title="Задача трёх тел"),
 BookRecommendation(id=14, title="Убик"),
 BookRecommendation(id=15, title="Планета КА-ПЭКС"),
 BookRecommendation(id=16, title="Страна багровых туч"),
 BookRecommendation(id=17, title="Странник по звездам"),
 BookRecommendation(id=18, title="Вечная жизнь Смерти"),
 BookRecommendation(id=19, title="Непобедимый"),
 BookRecommendation(id=20, title="Далекая Радуга"),
 ],
 BookCategory.SELF_HELP: [
 BookRecommendation(id=21, title="Семь навыков высокоэффективных людей"),
 BookRecommendation(id=22, title="Как завоёвывать друзей и оказывать влияние на людей"),
 BookRecommendation(id=23, title="Человек в поисках смысла"),
 BookRecommendation(id=24, title="Преимущество счастья."),
 BookRecommendation(id=25, title="Переключайтесь. Как меняться, когда это непросто"),
 BookRecommendation(id=26, title="Радикальное принятие."),
 BookRecommendation(id=27, title="Практикуйте себя: дневник"),
 BookRecommendation(id=28, title="Во всем можно разобраться"),
 BookRecommendation(id=29, title="Не оставайтесь на своей дневной работе"),
 BookRecommendation(id=30, title="Ни сы"),
 ],
}
class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):

 def Recommend(self, request, context):
  if request.category not in books_by_category:
   context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")
  books_for_category = books_by_category[request.category]
  num_results = min(request.max_results, len(books_for_category))
  books_to_recommend = random.sample(books_for_category, num_results)

  return RecommendationResponse(recommendations=books_to_recommend)
def serve():
 server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
 recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
 RecommendationService(), server
 )
 server.add_insecure_port("[::]:50051")
 server.start()
 server.wait_for_termination()
if __name__ == "__main__":
 serve()