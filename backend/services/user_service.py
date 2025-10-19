import pandas as pd

class UserService:
    """Gestiona información de usuarios"""
    
    def __init__(self, data_service):
        self.data = data_service
    
    def get_user_info(self, user_id):
        """Obtiene información del usuario"""
        user = self.data.users[self.data.users['User-ID'] == user_id]
        
        if user.empty:
            return {"error": "user_not_found"}
        
        user_ratings = self.data.ratings[self.data.ratings['User-ID'] == user_id]

        return {
            "user_id": user_id,
            "ubicacion": user['Location'].values[0],
            "edad": int(user['Age_cleaned'].values[0]) if pd.notna(user['Age_cleaned'].values[0]) else None,
            "libros_calificados": len(user_ratings),
            "rating_promedio": float(user_ratings['Book-Rating'].mean())
        }
    
    def get_statistics(self):
        """Estadísticas del sistema"""
        return {
            "total_usuarios": len(self.data.users),
            "total_libros": len(self.data.books),
            "total_ratings": len(self.data.ratings),
            "rating_promedio": float(self.data.ratings['Book-Rating'].mean()),
            "rango_rating": [0, 10]
        }